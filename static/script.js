async function analyze(){
    let text=document.getElementById("news").value;

    let res=await fetch("/predict",{
        method:"POST",
        headers:{"Content-Type":"application/x-www-form-urlencoded"},
        body:"news="+encodeURIComponent(text)
    });

    let data=await res.json();

    document.getElementById("result").innerText="Prediction: " + data.prediction;
    document.getElementById("confidence").innerText="Confidence: " + data.confidence + "%";
    document.getElementById("keywords").innerText="Keywords: " + data.keywords.join(", ");
    document.getElementById("highlightedText").innerHTML="Analysis: " + data.highlighted;
}