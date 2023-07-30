function ajaxCall(){

    $(document).ready(function(){
        function loadMessages(){
            $('#user-messages').html('').load(
                // send encoded query and type to url
                $('#user-messages').data('url'));
            return false;
        }
        function loadCandidates(){
            $('#job-candidates').html('').load(
                // send encoded query and type to url
                $('#job-candidates').data('url'));
            return false;
        }
        $('.fetch').on('click',function() {
            var nextUrl = $(this).data('action-next');
            console.log(nextUrl);
            $.ajax({
                url: nextUrl,
                method: 'GET',
                success: function(data) {
                    // load the div a url
                    loadMessages();
                    loadCandidates();
                },
                error: function(error) {
                    console.log(error);
                    loadMessages();
                    
                }
            });
        });
        
    });
}