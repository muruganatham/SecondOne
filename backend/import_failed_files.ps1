# Fixed Selective Import Script for TiDB Cloud
$MYSQL_PATH = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$TIDB_HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
$TIDB_PORT = "4000"
$TIDB_USER = "4U2ezhfza2XWo9c.root"
$TIDB_DB = "test"
$TIDB_PASS = "H445wifNVSAVW7ER"

$sqlFolder = "C:\Users\Admin\Documents\dumps\Dump20260213"
$env:MYSQL_PWD = $TIDB_PASS

$failedFiles = @(
    "coderv4_standard_qb_coding_validations.sql",
    "coderv4_srec_2026_1_coding_result.sql",
    "coderv4_srec_2025_2_coding_result.sql",
    "coderv4_routines.sql"
)

Write-Host "Starting Power-Fix Import for 4 files..."

# Configuration commands
$initSql = "SET SESSION tidb_txn_entry_size_limit = 125829120; SET SESSION max_allowed_packet = 134217728; SET FOREIGN_KEY_CHECKS=0;"
$initFile = Join-Path $env:TEMP "tidb_init_simple.sql"
$initSql | Out-File -FilePath $initFile -Encoding utf8

foreach ($fileName in $failedFiles) {
    $filePath = Join-Path $sqlFolder $fileName
    if (Test-Path $filePath) {
        Write-Host "Importing $fileName..." -NoNewline
        
        # Use Get-Content to stream both files into mysql.exe
        Get-Content $initFile, $filePath | & $MYSQL_PATH --host=$TIDB_HOST --port=$TIDB_PORT --user=$TIDB_USER --ssl-mode=REQUIRED --default-character-set=utf8mb4 $TIDB_DB
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " OK" -ForegroundColor Green
        } else {
            Write-Host " FAILED" -ForegroundColor Red
        }
    } else {
        Write-Host " File not found: $fileName" -ForegroundColor Yellow
    }
}

Write-Host "Done!"
