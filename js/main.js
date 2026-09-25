const API="https://essa-hwxl.onrender.com";
document.getElementById("year").textContent=new Date().getFullYear();
const menu=document.getElementById("mobileMenu");
if(menu) menu.onclick=()=>document.querySelector(".navbar").classList.toggle("open");

async function loadEvents(){
 const box=document.getElementById("eventsContainer"); if(!box)return;
 try{
  const r=await fetch(API+"/api/events/"); if(!r.ok)throw new Error();
  const events=await r.json();
  box.innerHTML=events.slice(0,3).map(e=>`
   <article class="event-card">
    <div class="event-image"><img src="${e.image?API+e.image:"assets/images/event-placeholder.jpg"}" alt="${e.title}"></div>
    <div class="event-info"><span>${e.date?new Date(e.date).toLocaleDateString("en-IN",{day:"numeric",month:"long",year:"numeric"}):"DATE TBA"}</span>
    <h3>${e.title}</h3><p>${e.description||"ESSA event and activity."}</p></div>
   </article>`).join("") || "<p>No upcoming events available.</p>";
 }catch(e){box.innerHTML="<p>Events will appear here when the backend is running.</p>"}
}
loadEvents();
