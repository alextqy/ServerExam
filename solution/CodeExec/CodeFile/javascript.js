var result = {
    RunTime: 0,
    Memory: 0,
    Result: ""
};

function main(){
    try{
        [CODE]
    }catch (error){
        return error.message;
    }
}

var start = (new Date()).valueOf();
result.Result = main().toString();
var end = (new Date()).valueOf();
result.RunTime = end-start;

console.log(JSON.stringify(result));