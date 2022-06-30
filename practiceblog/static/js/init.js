(function($){
  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
  document.addEventListener('DOMContentLoaded', function() {
   var elems = document.querySelectorAll('.fixed-action-btn');
   var instances = M.FloatingActionButton.init(elems, options);
 });
 document.addEventListener('DOMContentLoaded', function() {
      var elems = document.querySelectorAll('.sidenav');
      var instances = M.Sidenav.init(elems, {});
    });

    document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, options);
  });

  $(document).ready(function(){
    $('.collapsible').collapsible();
  });


 // Or with jQuery

 $(document).ready(function(){
   $('.fixed-action-btn').floatingActionButton();
 });

 $(document).ready(function(){
   $('select').formSelect();
 });
 $(document).ready(function(){
    $('.modal').modal();
  });
  (document).ready(function(){
    $('.tap-target').tapTarget();
  });
})(jQuery); // end of jQuery name space
