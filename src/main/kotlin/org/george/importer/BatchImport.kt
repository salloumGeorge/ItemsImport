package org.george.importer

import com.opencsv.CSVReader
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Service
import java.io.FileReader
import java.time.Instant
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import java.util.*

@Service
class BatchImport(private val jdbcTemplate: JdbcTemplate) {

    fun import(csvFilePath: String, batchSize: Int = 10000): ImportResult{

        val startMark: String = DateTimeFormatter
            .ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS")
            .withZone(ZoneOffset.UTC)
            .format(Instant.now())


        val reader = CSVReader(FileReader(csvFilePath))
        val records = reader.readAll()
        records.removeAt(0)
        val startTime = System.currentTimeMillis()

        var count = 0;
        var totalExecutionTime = 0L;



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
        return ImportResult(count, time, totalExecutionTime.toDouble()/count.toDouble(), startMark)
    }
}