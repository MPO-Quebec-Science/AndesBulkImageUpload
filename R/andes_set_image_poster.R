library(httr2)
library(jsonlite)


get_cookie <- function(sessionid, csrftoken) {
    #' This function should return a well formed cookie with the sessionid and csrf token
    #' See README.md for details
    #' @param sessionid The session ID string.
    #' @param csrftoken The CSRF token string.
    #' @return A named list representing the cookie.
    #' 
    cookie <- list(
        sessionid = sessionid,
        csrftoken = csrftoken
    )
    return(cookie)
}


get_form_payload <- function(csrfmiddlewaretoken, sample_id) {
    #' Create form payload for image upload
    #' @param csrfmiddlewaretoken The CSRF middleware token string.
    #' @param sample_id The sample/set ID integer.
    #' @return A named list representing the form payload.
    #'
    payload <- list(
        sample = sample_id,
        csrfmiddlewaretoken = csrfmiddlewaretoken
    )
    return(payload)
}


post_image <- function(set_id, fname, sessionid, csrftoken, csrfmiddlewaretoken, server_url) {
    #' Post a set image to the Andes server.
    #' @param set_id The ID (integer) of the set to which the image belongs.
    #' @param fname The path and name (string) to the image file to be posted.
    #' @param sessionid The session ID string.
    #' @param csrftoken The CSRF token string.
    #' @param csrfmiddlewaretoken The CSRF middleware token string.
    #' @param server_url The server URL string.
    #' @return status_code The HTTP status code of the response.
    #'
    api_path <- "/api/images/"
    
    if (is.null(set_id) || is.null(fname)) {
        stop("Both set_id and fname must be provided.")
    }
    
    if (!file.exists(fname)) {
        stop(paste("File does not exist:", fname))
    }
    
    # Create the request
    url <- paste0(server_url, api_path)
    
    # Get cookies and form payload
    cookies <- get_cookie(sessionid, csrftoken)
    form_data <- get_form_payload(csrfmiddlewaretoken, set_id)
    
    # Make the POST request
    tryCatch({
        req <- request(url) %>%
            req_cookies(!!!cookies) %>%
            req_body_multipart(
                sample = form_data$sample,
                csrfmiddlewaretoken = form_data$csrfmiddlewaretoken,
                image = curl::form_file(fname)
            )
        
        resp <- req_perform(req)
        status_code <- resp_status(resp)
        
        if (status_code == 201) {
            cat("Successfully uploaded:", fname, "for set_id:", set_id, "\n")
        } else {
            cat("Error uploading:", fname, "- Status code:", status_code, "\n")
        }
        
        return(status_code)
        
    }, error = function(e) {
        cat("Error posting image:", e$message, "\n")
        return(NULL)
    })
}


#' Bulk upload images from a directory
#' @param image_path The directory path containing images
#' @param sets_csv_path Path to the CSV file containing set mappings
#' @param sessionid The session ID string
#' @param csrftoken The CSRF token string
#' @param csrfmiddlewaretoken The CSRF middleware token string
#' @param server_url The server URL string
#' @param file_pattern The pattern to match image files (default: "*.jpg")
#' @return None (prints status messages)
#'
bulk_upload_images <- function(image_path, sets_csv_path, sessionid, csrftoken, 
                              csrfmiddlewaretoken, server_url, file_pattern = "*.jpg") {
    
    # Read the sets CSV file
    if (!file.exists(sets_csv_path)) {
        stop(paste("CSV file does not exist:", sets_csv_path))
    }
    
    sets <- read.csv(sets_csv_path, stringsAsFactors = FALSE)
    
    # Get list of image files
    image_files <- list.files(image_path, pattern = gsub("\\*", ".*", file_pattern), full.names = TRUE)
    
    if (length(image_files) == 0) {
        cat("No image files found in:", image_path, "\n")
        return()
    }
    
    # Sort files
    image_files <- sort(image_files)
    
    # Process each file
    for (file in image_files) {
        filename <- basename(file)
        
        # Parse set_number from filename (assuming format: mission_zone_setnumber_imagenumber.jpg)
        filename_parts <- strsplit(tools::file_path_sans_ext(filename), "_")[[1]]
        
        if (length(filename_parts) < 3) {
            cat("Warning: Cannot parse set number from filename:", filename, "\n")
            next
        }
        
        set_num <- as.integer(filename_parts[3])
        
        if (is.na(set_num)) {
            cat("Warning: Invalid set number in filename:", filename, "\n")
            next
        }
        
        # Map to set_id from CSV
        matching_rows <- sets[sets$set_number == set_num, ]
        
        if (nrow(matching_rows) == 0) {
            cat("Warning: No matching set_id found for set_number:", set_num, "\n")
            next
        }
        
        set_id <- matching_rows$set_id[1]
        
        cat("Processing:", filename, "- Set number:", set_num, "- Set ID:", set_id, "\n")
        
        # Post the image
        status <- post_image(set_id, file, sessionid, csrftoken, csrfmiddlewaretoken, server_url)
        
        # Optional: add a small delay to avoid overwhelming the server
        Sys.sleep(0.1)
    }
}


# Example usage configuration
# SERVER_URL <- "http://iml-science-4.ent.dfo-mpo.ca:25007"
# SERVER_URL <- "http://localhost:8000"
# IMAGE_PATH <- '\\\\stockage-crabe.ent.dfo-mpo.ca\\stockage\\Photos BSM 2025\\andes'

# Example tokens (replace with actual values)
# csrftoken <- "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# sessionid <- "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# csrfmiddlewaretoken <- "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Example usage:
# bulk_upload_images(
#     image_path = IMAGE_PATH,
#     sets_csv_path = "IML2025007_set_export.csv",
#     sessionid = sessionid,
#     csrftoken = csrftoken,
#     csrfmiddlewaretoken = csrfmiddlewaretoken,
#     server_url = SERVER_URL
# )