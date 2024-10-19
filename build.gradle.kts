plugins {
    kotlin("jvm") version "1.9.24"
    application
    id("com.github.johnrengelman.shadow") version "8.1.0"
}

group = "org.george"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.jetbrains.kotlin:kotlin-test")
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(17)
}

application {
    mainClass.set("MainKt") // Update this if your main class is in a package, e.g., "org.george.MainKt"
}

tasks.jar {
    manifest {
        attributes(
            "Main-Class" to application.mainClass.get() // Set the main class in the manifest
        )
    }
}