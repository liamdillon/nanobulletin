function confirmEmptyContent() {
    resp = confirm("Are you sure you want to submit a post with no content?");

    if(resp) return true;
    else return false;
};