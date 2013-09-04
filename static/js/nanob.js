function confirmEmptyContent() {
    var content = document.forms["post_form"]["content"].value;
    console.log(content);
    if (content==null || content == "") {
	resp = confirm("Are you sure you want to submit a post with no content?");
    }
    if(resp) return true;
    else return false;
};