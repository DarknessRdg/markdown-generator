#include <iostream>
using namespace std;


/**
 * Documentation here
 *
 * **Args**:
 *      - `number`: Integer
 * **Returns**:
 *      - `Float`: Number's square.
 */
float square(int number) {
    return number * number;
}

/**
 * Documentation here
 *
 * **Args**:
 *      - `number`: Double
 * **Returns**:
 *      - `Float`: Number's square.
 */
float square2(double number) {
    return number * number;
}


/**
 * Class docs here
 *
 * **Attributes**:
 *      - `x`: Integer
 *      - `y`: Integer
 */
class XY {
private:
    int x, y;

    /**
     * Empty Constructor here
     */
    XY() {}

    /**
     * Filled constructor here
     * **Args**:
     *      - X: Integer. Coordinate X
     *      - Y: Integer. Coordinate Y
     */
    XY(int x, int x) {}

    /**
     * Returns x * y
     */
    int multiply() { return this->x * this->y; }

    /**
     * Print position formatted.
     */
    void print() {
        cout << "(" << x << "," << y << ")" << endl;
    }
}

int main() {
    return 0;
}