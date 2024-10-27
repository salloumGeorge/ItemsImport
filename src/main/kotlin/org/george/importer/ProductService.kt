package org.george.importer

import com.opencsv.CSVReader
import org.george.model.Product
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Service
import java.io.FileReader
import java.util.UUID

@Service
class ProductService(private val jdbcTemplate: JdbcTemplate) {

    fun importProductsOneByOne(csvFilePath: String): ImportResult {
        val reader = CSVReader(FileReader(csvFilePath))
        val records = reader.readAll()
        val startTime = System.currentTimeMillis()

        //skip header
        records.removeAt(0)

        var count = 0;
        var totalExecutionTime = 0L;
        records.forEach { record ->
            val product = Product(
                UUID.randomUUID(),
                name = record[0],
                description = record[1],
                price =  record[2].toDouble()
            )


            val queryStarTime = System.currentTimeMillis()
            jdbcTemplate.update(
                "INSERT INTO products (id, name, description, price) VALUES (?, ?, ?, ?)",
               product.id, product.name, product.description, product.price
            )
            val queryEndTime = System.currentTimeMillis()
            val queryTime = queryEndTime - queryStarTime;
            count++;
            totalExecutionTime += queryTime;
        }

        val endTime = System.currentTimeMillis()
        val time = endTime - startTime
        reader.close()
        return ImportResult(count, time, totalExecutionTime.toDouble() / count.toDouble());
    }

    fun importProductsInBatches(csvFilePath: String, batchSize: Int = 10000): ImportResult {
        val reader = CSVReader(FileReader(csvFilePath))
        val records = reader.readAll()
        val startTime = System.currentTimeMillis()

        var count = 0;
        var totalExecutionTime = 0L;

        records.removeAt(0)
        records.chunked(batchSize).forEach { batch ->
            val sql = "INSERT INTO products (id, name, description, price) VALUES (?, ?, ?, ?)"
            val batchArgs = batch.map { record ->
                arrayOf(UUID.randomUUID(), record[0], record[1], record[2].toDouble())
            }

            val queryStarTime = System.currentTimeMillis()
            jdbcTemplate.batchUpdate(sql, batchArgs)
            val queryEndTime = System.currentTimeMillis()
            val queryTime = queryEndTime - queryStarTime;
            count++;
            totalExecutionTime += queryTime;


        }

        val endTime = System.currentTimeMillis()
        val time = endTime - startTime
        reader.close()
        return ImportResult(count, time, totalExecutionTime.toDouble()/count.toDouble())
    }

}
