/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



    $(function() {
    
    $('#id_sector').on('change',function(event){

        event.preventDefault();
        var requestData = {sector: $(this).val()}
        $.get('/provide_keywords', requestData, function(data) {
            alert(data);
            $('#id_keywords').html(data);
        });
    });
    });