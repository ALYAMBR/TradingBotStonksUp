FROM maven:3.8.6-eclipse-temurin-11 as build
COPY src /home/app/src
COPY pom.xml /home/app
RUN mvn -f /home/app/pom.xml clean package


FROM eclipse-temurin:11
COPY --from=build /home/app/target/moex-1.0-SNAPSHOT-jar-with-dependencies.jar backend
CMD ["java", "-jar", "backend"]