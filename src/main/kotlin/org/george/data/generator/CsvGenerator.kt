package org.george.data.generator

import java.io.File
import java.io.FileWriter
import java.util.UUID

class CsvGenerator(
    private val filename: String,
    private val name: String,
    private val description: String,
    private val price: Double
) {

    fun generateCsv(numRecords: Int) {
        val file = File(filename)
        FileWriter(file).use { writer ->
            // Write CSV header
            writer.append("name,description,price\n")

            for (i in 1..numRecords) {
                // Generate a new UUID for each record
                val id = UUID.randomUUID().toString()
                writer.append("$name,$description,$price\n")
            }
        }
    }
}
