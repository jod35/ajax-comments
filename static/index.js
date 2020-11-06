const commentButton=document.querySelector("#comment-btn");
const commentInput=document.querySelector("#comment");
const commentSection=document.querySelector(".comments");
const getCommentButton=document.querySelector("#fetch-comments");
let Xhttp=new XMLHttpRequest();

function Comment(comment){
    this.comment=comment;
}

function createComment(value){
    return new Comment(value);
}

function startRequest(){
    Xhttp.onreadystatechange=handleStateChange();
    Xhttp.open("POST","/add_comment",true);
    Xhttp.setRequestHeader("Content-Type","application/json");

    let newCommentInJSON=JSON.stringify(createComment(commentInput.value));
    Xhttp.send(newCommentInJSON);

    // 

}

function getComments(){
    Xhttp.onreadystatechange=handlesentCommentState();
    Xhttp.open("GET",'/get_comments',true);
    Xhttp.send(null);
}

function handlesentCommentState(){
    if(Xhttp.readyState==4){
        if(Xhttp.status==200){
            let commentsAsJSON=JSON.parse(Xhttp.responseText);
            commentSection.innerHTML=`<p>${commentsAsJSON.comments[0]}</p>`;
            Xhttp.abort();
        }
    }
}

function handleStateChange(){
    if(Xhttp.readyState ==4){
        if(Xhttp.status ==200){
            let responseAsObject=JSON.parse(Xhttp.responseText);
            commentSection.innerHTML=responseAsObject;
            console.log(responseAsObject.comment);
            Xhttp.abort();
        }
    }
    
}


getCommentButton.addEventListener('click',getComments);
commentButton.addEventListener('click',startRequest);