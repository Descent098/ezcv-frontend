
  function changeTheme(){
    // Get the current state of which theme is displayed
    whichView = localStorage.getItem('theme');
    if (whichView === null){
        localStorage.setItem('theme', "dark")
        whichView = 'dark';
    }
    var stylesheet = document.getElementById("themeCSS");
    const themeIndicator = document.getElementById("themeIndicator");
    const darkTheme = "/bootstrap-dark.css";
    const lightTheme = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css";

    if(localStorage.getItem('theme') === "dark"){
    localStorage.setItem('theme', "light")
    stylesheet.href = lightTheme;
    themeIndicator.innerHTML = '☀️  Light Theme';
    } else {
    localStorage.setItem('theme', "dark")
    stylesheet.href = darkTheme;
    themeIndicator.innerHTML = '🌙  Dark Theme';
    }

  }


  function toggleView(){
    // Get the elements of the content view
    const accordionView = document.getElementById("accordion");
    const gridView = document.getElementById("gridView");
    const viewIndicator = document.getElementById("viewIndicator");

    // Get the current state of which view is displayed
    whichView = localStorage.getItem('view');
    console.log(whichView);
  if(null === whichView){
    accordionView.hidden = false;
    gridView.hidden = true;
    localStorage.setItem('view', 'accordion')
    console.log("here");
    viewIndicator.innerHTML = '<i class="bi bi-journal-arrow-down"></i>  Accordion View';
  }else if (whichView ==="accordion"){
    accordionView.hidden = true;
    gridView.hidden = false;
    localStorage.setItem('view', 'grid')
    viewIndicator.innerHTML = '<i class="bi bi-grid-3x3"></i>  Grid View';
    }else{
    accordionView.hidden = false;
    gridView.hidden = true;
    localStorage.setItem('view', 'accordion')
    viewIndicator.innerHTML = '<i class="bi bi-journal-arrow-down"></i>  Accordion View';
    }
    
  }