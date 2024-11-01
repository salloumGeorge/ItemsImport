package org.george.importer

import org.springframework.stereotype.Service

@Service
class ProductService(
    private val threadBatchImport: MultiThreadBatchImport,
    private val singleFileImport: SingleFileImport,
    private val batchImport: BatchImport
) {

    fun importProductsOneByOne(csvFilePath: String): ImportResult {
        return singleFileImport.importSingle(csvFilePath)
    }

    fun importProductsInBatches(csvFilePath: String, batchSize: Int = 10000): ImportResult {
        return batchImport.import(csvFilePath, batchSize)
    }

    fun importProductsInParallelBatches(filePath: String, batchSize: Int): ImportResult {
        return threadBatchImport.importProductsInParallelBatches(filePath, batchSize)
    }


}
