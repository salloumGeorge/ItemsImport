package org.george.api

import org.george.importer.ProductService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api")
class HelloController(private val productService: ProductService) {

    @GetMapping("/hello")
    fun hello(): String {
        return "Hello, Spring with Kotlin!"
    }

    @GetMapping("/import/one-by-one")
    fun importOneByOne(): String {
        val time = productService.importProductsOneByOne("./src/main/resources/products.csv")
        return time.toString()
    }

    @GetMapping("/import/sql-batch")
    fun importSqlBatch(): String {
        val time = productService.importProductsInBatches("./src/main/resources/products.csv", 50000)
        return time.toString()
    }
}
