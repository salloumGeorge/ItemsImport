package org.george.importer

import com.opencsv.CSVReader
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Service
import java.io.FileReader
import java.time.Instant
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import java.util.*
import java.util.concurrent.CompletableFuture

@Service
class MultiThreadBatchImport(private val jdbcTemplate: JdbcTemplate) {


    fun importProductsInParallelBatches(csvFilePath: String, batchSize: Int = 10000, poolSize: Int = 10): ImportResult {
        val startMark: String = DateTimeFormatter
            .ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS")
            .withZone(ZoneOffset.UTC)
            .format(Instant.now())

        val reader = CSVReader(FileReader(csvFilePath))
        val records = reader.readAll()
        records.removeAt(0)

        val startTime = System.currentTimeMillis()

        var sumResults = mutableListOf<CompletableFuture<Long>>()
        records.chunked(batchSize).forEach { batch ->
            val sql = "INSERT INTO products (id, name, description, price) VALUES (?, ?, ?, ?)"
            val batchArgs = batch.map { record ->
                arrayOf(UUID.randomUUID(), record[0], record[1], record[2].toDouble())
            }

            val supplyAsync: CompletableFuture<Long> = CompletableFuture.supplyAsync {
                insertBatch(sql, batchArgs)
            }
            sumResults.add(supplyAsync);
        }


        val times = mutableListOf<Long>();
        sumResults.forEach() {
            times.add(it.get())
        }


        val endTime = System.currentTimeMillis()
        val time = endTime - startTime
        reader.close()
        return ImportResult(times.size, time, times.average(), startMark);
    }

    private fun insertBatch(sql: String, batchArgs: List<Array<*>>): Long {
        val startTime = System.currentTimeMillis()
        jdbcTemplate.batchUpdate(sql, batchArgs)
        val endTime = System.currentTimeMillis()
        return endTime - startTime;
    }
}