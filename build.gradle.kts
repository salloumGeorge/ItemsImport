plugins {
    kotlin("jvm") version "1.9.24"
    application
   // id("com.github.johnrengelman.shadow") version "8.1.0"
    id("org.springframework.boot") version "3.3.4"
    id("org.jetbrains.kotlin.plugin.spring") version "2.0.21"
}

group = "org.george"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation ("org.springframework.boot:spring-boot-starter-web:3.3.4")
    implementation("org.springframework.boot:spring-boot-starter-jdbc:3.3.4")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    testImplementation("org.jetbrains.kotlin:kotlin-test")
    implementation("org.postgresql:postgresql:42.7.2")
    implementation("com.opencsv:opencsv:5.7.1")
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(17)
}

application {
    mainClass.set("org.george.KotlinSpringApplicationKt") // Update this if your main class is in a package, e.g., "org.george.MainKt"
}

/*
tasks.jar {
    manifest {
        attributes(
            "Main-Class" to application.mainClass.get() // Set the main class in the manifest
        )
    }
}*/
