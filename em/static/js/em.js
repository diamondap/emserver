$(function() {

    function attachModals() {
        $('span[data-modal]').click(function showModal(evnt) {
            var url = $(evnt.delegateTarget).attr('data-modal');
            console.log("Modal URL = " + url);
            $('#modal').modal({
                'remote': url,
                'show': true,
                'backdrop': true,
                'keyboard': true
            });
        });
    }

    //attachModals();
});
