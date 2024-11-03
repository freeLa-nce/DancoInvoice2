function extractMessagesFromContent(scriptContent) {
    // Decode the escaped characters
    const decodedContent = scriptContent
        .replace(/\\x3C/g, '<') // Replace escaped < with actual <
        .replace(/\\x3E/g, '>'); // Replace escaped > with actual >

    try {
        // Extract the JSON string part (between the brackets)
        const jsonStartIndex = decodedContent.indexOf('[');
        const jsonEndIndex = decodedContent.lastIndexOf(']') + 1;

        // If valid JSON brackets found
        if (jsonStartIndex !== -1 && jsonEndIndex !== -1) {
            const jsonString = decodedContent.substring(jsonStartIndex, jsonEndIndex);

            // Parse the extracted JSON string
            return JSON.parse(jsonString);
        } else {
            console.error("No valid JSON found in the content.");
            return [];
        }
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return [];
    }
}



//Notiflix functions to display the messages
function SuccessAlert(Message) {
    Notiflix.Report.success(
        'Success',
        Message,
        'Okay',
    );
}

function ErrorAlert(Message) {
    Notiflix.Report.failure(
        'Failure',
        Message,
        'Okay',
    );
}

function WarningAlert(Message) {
    Notiflix.Report.warning(
        'Warning',
        Message,
        'Okay',
    );
}

function AccessDeniedAlert(Message) {
    Notiflix.Report.warning(
        'Access Denied!',
        Message,
        'Okay',
    );
}

function InfoAlert(Message) {
    Notiflix.Report.info(
        'Info',
        Message,
        'Okay',
    );
}

function ConfirmationAlert(actionFunc, CnfmMessage) {
    //
    Notiflix.Confirm.show(
        'Confirmation',
        CnfmMessage,
        'Yes',
        'No',
        function okCb() {
            actionFunc();
        },
        function cancelCb() {
        },
        {
        },
    )
}



