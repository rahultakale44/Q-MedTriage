// Simulate browser fetch to test exact behavior
const API_URL = "http://localhost:8000";

async function testPrediction() {
    try {
        // Read a genuine chest X-ray file
        const fs = require('fs');
        const FormData = require('form-data');
        
        const imagePath = 'data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg';
        const fileBuffer = fs.readFileSync(imagePath);
        
        const formData = new FormData();
        formData.append('file', fileBuffer, {
            filename: 'chest_xray.jpeg',
            contentType: 'image/jpeg'
        });
        
        console.log('Sending request to:', `${API_URL}/predict`);
        
        const fetch = require('node-fetch');
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData,
            headers: formData.getHeaders()
        });
        
        console.log('Status:', response.status);
        console.log('OK:', response.ok);
        
        const data = await response.json();
        console.log('\nResponse data:');
        console.log('  success:', data.success);
        console.log('  error:', data.error);
        console.log('  prediction_label:', data.prediction_label);
        console.log('  validation:', data.validation);
        
        // Simulate frontend logic
        if (response.status === 400 && data.error === "unsupported_image") {
            console.log('\n>>> FRONTEND: validationError = TRUE');
            console.log('>>> FRONTEND: Show "Invalid Image"');
        } else if (!response.ok) {
            console.log('\n>>> FRONTEND: validationError = FALSE');
            console.log('>>> FRONTEND: Show "Analysis Interrupted" (system error)');
        } else if (!data.success) {
            console.log('\n>>> FRONTEND: validationError = FALSE');
            console.log('>>> FRONTEND: Show "Analysis Interrupted" (data.success false)');
        } else {
            console.log('\n>>> FRONTEND: SUCCESS');
            console.log('>>> FRONTEND: Start visual pipeline');
        }
        
    } catch (error) {
        console.error('\nFETCH ERROR:', error.message);
        console.log('>>> FRONTEND: Network error (not validation)');
    }
}

testPrediction();
