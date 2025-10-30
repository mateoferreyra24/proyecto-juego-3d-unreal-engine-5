# **🛠️ Herramienta de Gestión de Modos de Juego (Python/Tkinter)**

Esta herramienta está diseñada para que el diseñador de juegos defina y balancee los modos de juego sin necesidad de editar archivos directamente. La salida principal es el archivo modos.json, que debe ser importado y consumido por Unreal Engine.

## **🎯 Principios Clave para Unreal Developers**

### **1\. Clave Principal: ID (UUID)**

**IMPORTANTE:** Nunca referencies un modo de juego por su nombre. El nombre puede cambiar por razones de localización o diseño.

* **Utiliza siempre el campo id (UUID)** como clave de búsqueda (Primary Key) en Unreal.  
* Este id es un string inmutable que garantiza la unicidad del modo en todo el proyecto.

### **2\. Archivo de Datos**

Los datos se guardan en el archivo **modos.json**. Este archivo es un *Array de Objetos JSON*, donde cada objeto es un modo de juego.

\[  
    {  
        "id": "a9e5b0c8-4e8f-4d9a-9e1b-2c3f8e7d6a4c",  
        "nombre": "Supervivencia",  
        "descripcion": "Lucha contra hordas infinitas. Poca munición, muchos enemigos.",  
        "dificultad": "Extrema",  
        "enemigos": 50,  
        "recursos": "Escasos"  
    }  
    // ... más modos  
\]

### **3\. Consumo en Unreal Engine**

Se recomienda consumir este JSON utilizando una **Tabla de Datos (Data Table)** de Unreal, donde el id (UUID) de la herramienta se mapee como la *Row Name* de la tabla.

* **Paso 1:** El diseñador debe usar el botón **Guardar JSON** después de hacer cambios.  
* **Paso 2:** El programador debe **copiar el archivo modos.json** al directorio de contenido de Unreal o utilizar un script de importación para actualizar la Data Table.  
* **Paso 3:** La lógica del juego debe buscar los parámetros del modo (como enemigos o recursos) basándose en el **ID del Modo** activo.

## **📝 Guía de Uso de la Herramienta**

### **A. Crear/Añadir un Modo Nuevo**

1. Asegúrate de que el botón principal muestre **"Crear Nuevo Modo"** (color verde).  
2. El campo **ID (UUID)** se habrá generado automáticamente con un valor nuevo y único.  
3. Rellena todos los campos (Nombre, Descripción, etc.).  
4. Haz clic en **"Crear Nuevo Modo"**.  
5. **OBLIGATORIO:** Haz clic en **"Guardar JSON"** para escribir los cambios en el archivo.

### **B. Editar un Modo Existente**

1. En la **"Lista de Modos"**, haz **doble clic** sobre el modo que deseas modificar.  
2. Los datos del modo se cargarán en los campos de entrada.  
3. El botón principal cambiará a **"Guardar Cambios"** (color naranja).  
4. Realiza las modificaciones necesarias.  
5. Haz clic en **"Guardar Cambios"**.  
6. **OBLIGATORIO:** Haz clic en **"Guardar JSON"** para que los cambios sean persistentes.

### **C. Campos del Modo**

| Campo | Tipo de Dato | Propósito | Notas para Unreal |
| :---- | :---- | :---- | :---- |
| **id** | String (UUID) | **Clave de referencia única.** | Usar como Row Name o clave de búsqueda. |
| **nombre** | String | Nombre legible del modo. | Usado principalmente en la UI. |
| **descripcion** | String | Descripción del modo de juego. | Usado en menús y pantallas de carga. |
| **dificultad** | String | Nivel de dificultad (Fácil, Media, Extrema). | Útil para lógica de escalado de IA. |
| **enemigos** | Entero (int) | Cantidad inicial de enemigos. | Debe ser consumido como un entero. |
| **recursos** | String | Nivel de recursos disponibles (Escasos, Abundantes). | Útil para inicializar el inventario o generación de *loot*. |

*Si encuentras errores en la herramienta, contacta al programador Python para que la revise.*