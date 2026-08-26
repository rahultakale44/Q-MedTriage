# Test Q-MedTriage API with PowerShell
$apiUrl = "http://localhost:8000/predict"

# Test paths
$normalImage = "data/archive (1)/chest_xray/chest_xray/test/NORMAL/IM-0001-0001.jpeg"
$pneumoniaImage = "data/archive (1)/chest_xray/chest_xray/test/PNEUMONIA/person100_bacteria_475.jpeg"

Write-Host "=" * 70
Write-Host "Testing Q-MedTriage API with PowerShell"
Write-Host "=" * 70

# Test 1: NORMAL X-ray
if (Test-Path $normalImage) {
    Write-Host "`n1. Testing with NORMAL X-ray:"
    Write-Host "-" * 70
    
    $fileBytes = [System.IO.File]::ReadAllBytes($normalImage)
    $fileName = Split-Path $normalImage -Leaf
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $contentType = "multipart/form-data; boundary=$boundary"
    
    $bodyLines = @(
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
        "Content-Type: image/jpeg",
        "",
        [System.Text.Encoding]::GetEncoding("ISO-8859-1").GetString($fileBytes),
        "--$boundary--"
    )
    
    $body = $bodyLines -join "`r`n"
    
    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Method Post -ContentType $contentType -Body $body
        Write-Host "✓ Status: Success"
        Write-Host "✓ Prediction: $($response.prediction_label)"
        Write-Host "✓ Confidence: $([math]::Round($response.confidence * 100, 2))%"
        Write-Host "✓ Inference time: $($response.inference_time_ms)ms"
        Write-Host "✓ Probabilities:"
        Write-Host "    NORMAL: $([math]::Round($response.probabilities.NORMAL * 100, 2))%"
        Write-Host "    PNEUMONIA: $([math]::Round($response.probabilities.PNEUMONIA * 100, 2))%"
    }
    catch {
        Write-Host "✗ Error: $_"
    }
}

# Test 2: PNEUMONIA X-ray
if (Test-Path $pneumoniaImage) {
    Write-Host "`n2. Testing with PNEUMONIA X-ray:"
    Write-Host "-" * 70
    
    $fileBytes = [System.IO.File]::ReadAllBytes($pneumoniaImage)
    $fileName = Split-Path $pneumoniaImage -Leaf
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $contentType = "multipart/form-data; boundary=$boundary"
    
    $bodyLines = @(
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
        "Content-Type: image/jpeg",
        "",
        [System.Text.Encoding]::GetEncoding("ISO-8859-1").GetString($fileBytes),
        "--$boundary--"
    )
    
    $body = $bodyLines -join "`r`n"
    
    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Method Post -ContentType $contentType -Body $body
        Write-Host "✓ Status: Success"
        Write-Host "✓ Prediction: $($response.prediction_label)"
        Write-Host "✓ Confidence: $([math]::Round($response.confidence * 100, 2))%"
        Write-Host "✓ Inference time: $($response.inference_time_ms)ms"
        Write-Host "✓ Probabilities:"
        Write-Host "    NORMAL: $([math]::Round($response.probabilities.NORMAL * 100, 2))%"
        Write-Host "    PNEUMONIA: $([math]::Round($response.probabilities.PNEUMONIA * 100, 2))%"
    }
    catch {
        Write-Host "✗ Error: $_"
    }
}

Write-Host "`n" + "=" * 70
Write-Host "API test complete"
Write-Host "=" * 70
