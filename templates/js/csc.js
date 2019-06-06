function initialize() {
    addcloud(); //为页面添加遮罩
    document.onreadystatechange = subSomething; //监听加载状态改变
}
 
function addcloud() {

    var bodyWidth = document.documentElement.clientWidth;
    var bodyHeight = Math.max(document.documentElement.clientHeight, document.body.scrollHeight);
    var bgObj = document.createElement("div" );
    bgObj.setAttribute( 'id', 'bgDiv' );
    bgObj.style.position = "absolute";
    bgObj.style.top = "0";
    bgObj.style.background = "#000000";
    bgObj.style.filter = "progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75" ;
    bgObj.style.opacity = "0.5";
    bgObj.style.left = "0";
    bgObj.style.width = bodyWidth + "px";
    bgObj.style.height = bodyHeight + "px";
    bgObj.style.zIndex = "10000"; //设置它的zindex属性，让这个div在z轴最大，用户点击页面任何东西都不会有反应|
    document.body.appendChild(bgObj); //添加遮罩
    var loadingObj = document.createElement("div");
    loadingObj.setAttribute( 'id', 'loadingDiv' );
    loadingObj.style.position = "absolute";
    loadingObj.style.top = bodyHeight / 2 - 32 + "px";
    loadingObj.style.left = bodyWidth / 2 + "px";
    loadingObj.style.background = "url(img/loading.gif)" ;
    loadingObj.style.width = "37px";
    loadingObj.style.height = "37px";
    loadingObj.style.zIndex = "10000"; 
    document.body.appendChild(loadingObj); //添加loading动画-
}
 
function removecloud() {
    $( "#loadingDiv").remove();
    $( "#bgDiv").remove();
}
 
function subSomething() {
    if (document.readyState == "complete" ) //当页面加载完毕移除页面遮罩，移除loading动画-
    {
        removecloud();
    }
}