package org.george.importer

import com.opencsv.CSVReader
import org.george.model.Product
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Service
import java.io.FileReader
import java.time.Instant
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import java.util.*

@Service
class SingleFileImport(private val jdbcTemplate: JdbcTemplate) {

    public fun importSingle(csvFilePath: String): ImportResult {

        val startMark: String = DateTimeFormatter
            .ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS")
            .withZone(ZoneOffset.UTC)
            .format(Instant.now())

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
                price = record[2].toDouble()
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
        return ImportResult(count, time, totalExecutionTime.toDouble() / count.toDouble(), startMark);
    }
}


