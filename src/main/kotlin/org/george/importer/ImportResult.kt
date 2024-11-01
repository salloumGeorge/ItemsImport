package org.george.importer

data class ImportResult(val executedQueries: Int ,
                        val totalTimeMs: Long,
                        val averageTimeMs: Double,
                        val startTime: String
    ){
}
