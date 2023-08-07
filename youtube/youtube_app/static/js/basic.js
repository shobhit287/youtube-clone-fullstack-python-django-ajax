let sidebar=document.querySelector('.sidebar');
let open_close=document.getElementById('hamburger-open-close');
let content=document.querySelector('.video-container');
function hamburger(){
sidebar.classList.toggle('hamburger');
if(sidebar.classList.contains('hamburger')){
    content.classList.toggle('content-width');
}
else{
    content.classList.remove('content-width');
}
}
document.addEventListener("click",function(event){
  
  if(!sidebar.contains(event.target)&&event.target!==open_close)
  {
    content.classList.remove('content-width');
    sidebar.classList.remove('hamburger');
  }
})



const suggestionList = $("#search-suggestions");
$('#search').on('input',function(){
let query=$(this).val();
if(query===''){
$('#search-suggestions').empty();
}
else{
    $.ajax({
        type:'GET',
        url:'/youtube/search-suggestion',
        data:{query:query},
        dataType:"json",
        encode:true,
    })
    .done(function(data){
       suggestionList.empty();
       data.forEach((video)=>{
           const li = `<li><a href="/youtube/search/${video.video_id}"><i class="fa-solid fa-magnifying-glass" ></i>${video.video_title}</a></li>`;
           suggestionList.append(li);
       });
    });
}
});