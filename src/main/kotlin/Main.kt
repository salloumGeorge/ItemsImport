import org.george.data.generator.CsvGenerator

fun main(args: Array<String>) {
    CsvGenerator("./src/main/resources/products.csv", "Product", "A product", 100.0)
        .generateCsv(100000);
}