$port = new-Object System.IO.Ports.SerialPort COM12,4000000,None,8,one

$code = @'
    [DllImport("user32.dll")]
     public static extern IntPtr GetForegroundWindow();
'@
Add-Type $code -Name Utils -Namespace Win32
$processLast = "-"

$array = Get-Content -Path @("page_list.txt")
foreach ($item in $array) {
    Write-Output $item
}



while(1){
    $hwnd = [Win32.Utils]::GetForegroundWindow()
    $process = Get-Process | 
        Where-Object { $_.mainWindowHandle -eq $hwnd } | 
        Select-Object processName;


    if ($process -notmatch $processLast){
        Write-Output $process
        $processLast = $process

        foreach($line in $array){
            if($line.Contains($process.ProcessName)){
                $args = $line.Split(",")
                $port.Open()
                $port.Write("3")
                $port.Write($args[1])
                $port.Close()
            } 
        }

    }
}