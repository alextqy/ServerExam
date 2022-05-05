<?php
header('Content-Type:application/json; charset=utf-8');
error_reporting(0);

$result['RunTime'] = 0;
$result['Memory'] = 0;
$result['Result'] = '';

register_shutdown_function('ShutdownFunc');
function ShutdownFunc(){
    if ($error = error_get_last()) {
        global $result;
        $result['Result'] = $error['message'] . ' in ' . $error['file'] . ' on line ' . $error['line'];
        Tojson($result);
    }
}

set_error_handler('CustomError');
function CustomError($type, $message, $file, $line){
    global $result;
    $result['Result'] = $message . ' in ' . $file . ' on ' . $line . ' line .';
    Tojson($result);
}

function Tojson($result){
    echo json_encode($result);
    exit();
}

function Run(){
    try{
        [CODE]
    }catch (Exception $e) {
        return $e->getMessage();
    }
}

$stime = microtime(true);

$result['Result'] = Run();

$etime = microtime(true);

$result['RunTime'] = round(($etime - $stime) * 1000,2);
$result['Memory'] = memory_get_usage();
Tojson($result);