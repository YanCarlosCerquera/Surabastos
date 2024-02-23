document.addEventListener('DOMContentLoaded', function () {
    var cellInput = document.getElementById('id_cell');
    
    // Define la longitud máxima para el campo
    var maxLength = 13;

    cellInput.addEventListener('input', function () {
        // Obtén el valor actual del campo
        var currentValue = this.value;
        
        // Verifica si el valor comienza con +57 y no se ha superado la longitud máxima
        if (currentValue.startsWith('+57') && currentValue.length <= maxLength) {
            return;
        }
        
        // Si el valor no comienza con +57 o se supera la longitud máxima, restaura el valor con +57
        var sanitizedValue = '+57' + currentValue.replace(/\D/g, ''); // Elimina caracteres no numéricos
        
        // Asegura que no supere la longitud máxima
        if (sanitizedValue.length > maxLength - 3) {
            sanitizedValue = sanitizedValue.slice(0, maxLength - 3);
        }

        // Actualiza el valor del campo
        this.value = sanitizedValue;
    });

    cellInput.addEventListener('focus', function () {
        // Si el campo está vacío o contiene solo el prefijo +57, muestra solo el prefijo +57
        if (this.value === '+57' || this.value === '+57 ') {
            this.value = '+57';
        }
    });

    // Inicializa el campo con +57 si está vacío
    if (cellInput.value === '') {
        cellInput.value = '+57';
    }
});
