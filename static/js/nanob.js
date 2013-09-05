function validatePost() {
    var content = document.forms["post_form"]["content"].value;
    var title = document.forms["post_form"]["title"].value;

    if (title==null || title=="") {
	alert("You can't make a post with no title");
	return false;
    }
    if (content==null || content=="") {
	resp = confirm("Are you sure you want to submit a post with no content?");
    }
    if(resp) return true;
    else return false;
};

function confirmDelete() {
    resp = confirm("Are you sure you want to delete this post?");
    return resp;
};