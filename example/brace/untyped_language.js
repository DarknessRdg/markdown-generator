/**
 * Documentation here
 *
 * **Args**:
 *      - `number`: Integer
 * **Returns**:
 *      - `Float`: Number's square.
 */
function square(number) {
    return number * number
}


/**
 * Documentation here
 *
 * **Args**:
 *      - `number`: Integer
 * **Returns**:
 *      - `Float`: Number's square.
 */
const square2 = (number) => {
    return number * number
};

/**
 * Documentation here
 *
 * **Args**:
 *      - `number`: Integer
 * **Returns**:
 *      - `Float`: Number's square.
 */
const square3 = number => number * number;

/**
 * Documentation here
 *
 * **Args**:
 *      - `number`: Integer
 * **Returns**:
 *      - `Float`: Number's square.
 */
const square4 = number => {
    return number * number;
};


/**
 * This is a function with nested function
 */
function nested(){
    /**
     * Child function
     */
    function child() {
        /**
         * Child2 function
         */
        function child__child(number, string, callback) {}
    }

    /**
     * Child function
     */
    function child2() {}
}


/**
 * Class docs here
 *
 * **Attributes**:
 *      - `x`: Integer
 *      - `y`: Integer
 */
class XY {
    /**
     * Filled constructor here
     * **Args**:
     *      - X: Integer. Coordinate X
     *      - Y: Integer. Coordinate Y
     */
    constructor (x, y) {}

    /** Inline docs here **/
    print(){

    }


    /**
     * Docs here
     * **Args**:
     *      - `a`: Integer
     *      - `b`: Integer
     */
    static distancia(a, b) {}
}

/**
 * Another class here
 */
class Square extends XY {

}