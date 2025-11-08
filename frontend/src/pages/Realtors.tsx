import React from "react";
import "@/styles/realtor.css";
import realtor1 from "@/assets/realtor1.jpg";
import realtor2 from "@/assets/realtor2.jpg";
import realtor3 from "@/assets/realtor3.jpg";
import realtor4 from "@/assets/realtor4.jpg";
import realtor5 from "@/assets/realtor5.jpg";

const dummyRealtors = [
  { name: "John Doe", image: realtor1, contact: "john.doe@example.com" },
  { name: "Jane Smith", image: realtor2, contact: "jane.smith@example.com" },
  { name: "Emily Johnson", image: realtor3, contact: "emily.johnson@example.com" },
  { name: "Michael Brown", image: realtor4, contact: "michael.brown@example.com" },
  { name: "Sarah Lee", image: realtor5, contact: "sarah.lee@example.com" },
];

export default function Realtors() {
  return (
    <main className="realtors-page">
      <h1 className="page-title">Our Partner Realtors</h1>
      <div className="realtors-grid">
        {dummyRealtors.map((realtor, index) => (
          <div key={index} className="realtor-card">
            <img src={realtor.image} alt={realtor.name} className="realtor-image" />
            <h2 className="realtor-name">{realtor.name}</h2>
            <p className="realtor-contact">Contact: {realtor.contact}</p>
            <button className="btn contact-btn">Contact</button>
          </div>
        ))}
      </div>
    </main>
  );
}