public class Demo {

    public static void main(String[] args) {
        Biryani myBiryani = new Biryani("Chicken", 1, true);
//        Biryani myBiryani = new Biryani();
//        myBiryani.proteinType = "Chicken";
//        myBiryani.noOfPlates = 1;
//        myBiryani.isSpicy = true;

        System.out.println(myBiryani.isSpicy);

        Biryani biryaniForViom = new Biryani("SoyaChunks", 2, true);
//        biryaniForViom.proteinType = "SoyaChunks";
//        biryaniForViom.noOfPlates = 2;
//        biryaniForViom.isSpicy = true;

        System.out.println(biryaniForViom.proteinType);

//        Constructor


        Square s1 = new Square(4);
        System.out.println(s1.getArea());
        System.out.println(s1.getArea());
    }

    private void test() {

    }

}

class Biryani {
    String proteinType;
    int noOfPlates;
    boolean isSpicy;

    // Constructor
    Biryani(String proteinType, boolean isSpicy, int noOfPlates) {
        this.proteinType = proteinType;
        this.noOfPlates = noOfPlates;
        this.isSpicy = isSpicy;
    }

    Biryani(String proteinType, boolean isSpicy) {
        this.proteinType = proteinType;
        this.noOfPlates = 1;
        this.isSpicy = isSpicy;
    }

}

class Square {
    int edge;
    double area = -1.0D;
    int perimeter = -1;

    public Square(int edge) {
        this.edge = edge;
    }

    public double getArea() {
        if (this.area < 0) {
            this.area = this.edge * this.edge;
        }
        return this.area;
    }

    public double getPerimeter() {
        if (this.perimeter < 0) {
            this.perimeter = 4 * this.edge;
        }
        return this.perimeter;
    }
}

class Circle {

    int radius;

    public Circle(int radius) {
        this.radius = radius;
    }
}
