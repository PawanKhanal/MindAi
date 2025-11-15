Write-Host "=== FINAL SYSTEM CHECK ==="

# Test 1: Health
Write-Host "`n1. Health Check:"
try {
    $health = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    Write-Host "   ✅ Status: $($health.StatusCode)"
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)"
}

# Test 2: Document Search
Write-Host "`n2. Document Search:"
$body = @{
    message = "What can the RAG system do?"
    session_id = "final_check"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat/query" -Method Post -Body $body -ContentType "application/json"
    Write-Host "   ✅ Response: $($result.response)"
    Write-Host "   ✅ Sources found: $($result.sources.Count)"
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)"
}

# Test 3: Booking
Write-Host "`n3. Interview Booking:"
$bookingBody = @{
    name = "Test User"
    email = "test@example.com"
    date = "2024-01-20"
    time = "14:30"
} | ConvertTo-Json

try {
    $booking = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat/book-interview" -Method Post -Body $bookingBody -ContentType "application/json"
    Write-Host "   ✅ Booking ID: $($booking.booking_id)"
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)"
}

Write-Host "`n=== CHECK COMPLETE ==="