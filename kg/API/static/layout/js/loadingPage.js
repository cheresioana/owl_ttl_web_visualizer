window.addEventListener('beforeunload', showLoadPage);
document.getElementById('searchForm').addEventListener('submit', showLoadPage);

function showLoadPage()
{
    $('#loading_page_text').text('Getting data from verified sources...')
    // Show page loading
    KTApp.showPageLoading();

}


function showLoadPageMoreResults()
{
    let element = $('#loading_page_text')
    element.text('Getting more data...')
    // Show page loading
    KTApp.showPageLoading();
}

function hideLoadingPage(){
    KTApp.hidePageLoading();
}

function completeSearch(searchKey)
{
    searchInput = $('#searchInput');
    searchForm = $('#searchForm');
    showLoadPage();
    searchInput.val(searchKey);
    searchForm.submit();


}