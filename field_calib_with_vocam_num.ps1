param (
    [string] $inputPath,
    [string] $outputPath,
    [int] $rows = 8,
    [int] $cols = 5,
    [float] $scale = 322,
    [int] $vocamNum  # New parameter for vocamNum
)

$localGraphDir = Join-Path $json.origin.localPath "Graphs" "xml6"
$localRunnerBuild = Join-Path $json.origin.localPath "builds" $json.origin.version

# Function to run the XML graph and modify parameters
function RunGraph($graphPath) {
    $exePath = "$($localRunnerBuild)\xmlgraphrunner.exe"
    Start-Process -NoNewWindow -Wait -FilePath $exePath -ArgumentList $graphPath
    Write-Host "Graph processing complete. Output files are in $outputFolder."
}

# Function to modify specific XML graph parameters
function ModifyGraphParameters($graphPath, $parameterName, $newValue) {
    [xml]$xmlConfig = Get-Content $graphPath

    $xmlConfig.genesis.mvxpipeline.filter | Where-Object { $_.name -eq "CalibrationAnalyzer" } | ForEach-Object {
        $_.parameters.parameter | Where-Object { $_.name -eq $parameterName } | ForEach-Object { $_.value = $newValue }
    }

    if ($parameterName -eq "config file") {
        $ecfgFile = Get-ChildItem "C:\nuc\stream$($vocamNum.ToString("D3"))_config.ecfg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        $xmlConfig.genesis.mvxpipeline.filter | Where-Object { $_.name -eq "MV4DCameraParamsFilter" } | ForEach-Object {
            $_.parameters.parameter | Where-Object { $_.name -eq $parameterName } | ForEach-Object { $_.value = $ecfgFile.FullName }
        }
    }

    $xmlConfig.Save($graphPath)
}

# Function to run the Calibration Analyzer function
function RunAnalyzer($inputPath, $outputPath, $graphName) {
    $originalGraph = Join-Path -Path $localGraphDir $graphName
    $outputFolder = Join-Path -Path $outputPath "original"
    mkdir $outputFolder -ea 0
    $copyGraph = Join-Path -Path $outputFolder ($graphName -replace '\.xml$', '_copy.xml')

    Copy-Item -Path $originalGraph -Destination $copyGraph
    ModifyGraphParameters $copyGraph "Results output file path" (Join-Path -Path $outputFolder "calibrationResults.csv")
    ModifyGraphParameters $copyGraph "Log file path" (Join-Path -Path $outputFolder "calibrationResults.log")
    RunGraph $copyGraph
}

# Function to run the Field Calibration Graph Out function
function RunFieldCalibrationGraphOut($inputPath, $outputPath) {
    $graph = Join-Path -Path $localGraphDir "fieldCalibrationGraphOut.xml"
    $outputFolder = Join-Path -Path $outputPath "new"
    mkdir $outputFolder -ea 0
    ModifyGraphParameters $graph "MVX File Path" $inputPath
    ModifyGraphParameters $graph "Output Path" $outputFolder
    RunGraph $graph
}

# Function to run the Calibration Analyzer After Field function
function RunAnalyzerAfterField($inputPath, $outputPath, $graphName) {
    $originalGraph = Join-Path -Path $localGraphDir $graphName
    $outputFolder = Join-Path -Path $outputPath "new"
    mkdir $outputFolder -ea 0
    $copyGraph = Join-Path -Path $outputFolder ($graphName -replace '\.xml$', '_copy.xml')

    Copy-Item -Path $originalGraph -Destination $copyGraph
    ModifyGraphParameters $copyGraph "Scale (mm)" $scale
    ModifyGraphParameters $copyGraph "Log file path" (Join-Path -Path $outputFolder "calibrationResults3.log")
    ModifyGraphParameters $copyGraph "Results output file path" (Join-Path -Path $outputFolder "calibrationResults3.csv")
    ModifyGraphParameters $copyGraph "MVX File Path" $inputPath
    ModifyGraphParameters $copyGraph "Circle Pattern Cols" $cols
    ModifyGraphParameters $copyGraph "Circle Pattern Rows" $rows
    ModifyGraphParameters $copyGraph "rig file" (Join-Path -Path $outputFolder "rig.txt")
    ModifyGraphParameters $copyGraph "colorrig file" (Join-Path -Path $outputFolder "colorrig.txt")
    ModifyGraphParameters $copyGraph "config file" ((Get-ChildItem "C:\nuc\stream$($vocamNum.ToString("D3"))_config.ecfg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName)
    ModifyGraphParameters $copyGraph "MVX File Path" (Join-Path -Path $outputFolder "new_mvx.mvx")
    RunGraph $copyGraph
}

# Function to run all three commands
function RunAllAnalyzerFieldAndAnalyzer($inputPath, $outputPath, $rows, $cols, $scale, $voc
