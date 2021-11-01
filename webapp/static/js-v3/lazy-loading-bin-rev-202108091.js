const iframes=document.querySelectorAll('iframe[loading="lazy bitchute"]')
iframes.forEach(function(e){e.src=e.dataset.src})