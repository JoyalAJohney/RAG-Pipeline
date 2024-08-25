import AWS from 'aws-sdk';
import { v4 as uuid } from 'uuid';
import express from 'express';

const app = express();
app.use(express.json());

// configure AWS
AWS.config.update({ 
    region: process.env.AWS_REGION,
    endpoint: process.env.AWS_ENDPOINT_URL,
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});


const s3 = new AWS.S3({
    s3ForcePathStyle: true,
    signatureVersion: 'v4',
});
const sqs = new AWS.SQS();

const S3_UPLOAD_BUCKET = process.env.S3_UPLOAD_BUCKET;
const PROCESSING_QUEUE_URL = process.env.PROCESSING_QUEUE_URL;


app.get('/upload/get-presigned-url', async (req, res) => {
    console.log('GET /upload/get-presigned-url');

    const fileName = req.query.fileName;
    const fileType = req.query.fileType;

    if (!fileName || !fileType) {
        return res.status(400).json({ message: 'fileName and fileType are required' });
    }

    const jobId = uuid();
    const s3Key = `${jobId}_${fileName}`;

    const params = {
        Bucket: S3_UPLOAD_BUCKET,
        Key: s3Key,
        ContentType: fileType,
        Expires: 60 * 5, // expires in 5 minutes
    };

    s3.getSignedUrl('putObject', params, (err, url) => {
        if (err) {
            console.error('Error generating presigned URL:', err);
            return res.status(500).json({ message: 'Error generating presigned URL' });
        }
        console.log('sending presigned URL:', url);
        res.json({ 
            jobId: jobId,
            s3Key: s3Key,
            presignedUrl: url, 
        });
    });
});


app.post('/upload/initiate-processing', async (req, res) => {
    console.log('POST /upload/initiate-processing');

    const { s3Key, jobId } = req.body;

    if (!s3Key || !jobId) {
        return res.status(400).json({ message: 's3Key or jobId is missing' });
    }

    try {
        // Send message to SQS
        await sqs.sendMessage({
          QueueUrl: PROCESSING_QUEUE_URL,
          MessageBody: JSON.stringify({
            job_id: jobId,
            key: s3Key,
            bucket: S3_UPLOAD_BUCKET,
          }),
        }).promise();
    
        res.json({ message: 'Ingestion pipeline initiated', job_id: jobId });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ message: `An error occurred: ${error.message}` });
      }
});


const PORT = process.env.UPLOAD_SERVICE_PORT || 8000;
app.listen(PORT, () => {
  console.log(`Upload service listening on port ${PORT}`);
});