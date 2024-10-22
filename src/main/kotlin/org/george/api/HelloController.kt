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
        return "Importing products one by one... took ${time/1000} s"
    }
}
