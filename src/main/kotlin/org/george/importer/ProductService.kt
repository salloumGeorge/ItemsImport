package org.george.importer

import com.opencsv.CSVReader
import org.george.model.Product
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Service
import java.io.FileReader
import java.util.UUID

@Service
class ProductService(private val jdbcTemplate: JdbcTemplate) {

    fun importProductsOneByOne(csvFilePath: String): Long {
        val reader = CSVReader(FileReader(csvFilePath))
        val records = reader.readAll()
        val startTime = System.currentTimeMillis()

        //skip header
        records.removeAt(0)

        records.forEach { record ->
            val product = Product(
                UUID.randomUUID(),
                name = record[0],
                description = record[1],
                price =  record[2].toDouble()
            )
            jdbcTemplate.update(
                "INSERT INTO products (id, name, description, price) VALUES (?, ?, ?, ?)",
               product.id, product.name, product.description, product.price
            )
        }

        val endTime = System.currentTimeMillis()
        val time = endTime - startTime
        println("Time taken for one-by-one import: $time ms")
        reader.close()
        return time;
    }

}
