// Mendapatkan elemen form dan hasil input
const form = document.getElementById("inputForm");
const resultName = document.getElementById("resultName");
const resultAge = document.getElementById("resultAge");

// Menangani pengiriman form
form.addEventListener("submit", function(event) {
    event.preventDefault(); // Mencegah reload halaman saat form dikirim
    
    // Mendapatkan nilai input
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;

    // Menampilkan hasil input pada card kanan
    resultName.textContent = `Nama: ${name}`;
    resultAge.textContent = `Usia: ${age}`;
    
    // Membersihkan input form
    form.reset();
});
