function valida(){
   var valor = document.getElementById('quadra').value;
   if (valor == 'society'){
    document.getElementById('foto').src = 'society_quadra.png' 
  
   }
   
   if (valor == 'areia'){
    document.getElementById('imagem2').src = "areia_quadra.png";

    }

    if (valor == 'salao'){
        document.getElementById('imagem3').src = "salao_quadra.jpg";
   
    }
    if (valor == 'volei'){
        document.getElementById('imagem4').src = "volei_quadra.jpg";
   
    }


}
