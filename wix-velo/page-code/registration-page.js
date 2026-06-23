import { submitRegistration } from 'backend/registration.web';

const HTML_COMPONENT_ID = '#registrationHtml';

$w.onReady(() => {
  const formFrame = $w(HTML_COMPONENT_ID);

  formFrame.onMessage(async (event) => {
    const message = event.data || {};

    if (message.type !== 'plan-t-registration-submit') {
      return;
    }

    formFrame.postMessage({
      type: 'plan-t-registration-status',
      status: 'sending'
    });

    try {
      await submitRegistration(message.payload);
      formFrame.postMessage({
        type: 'plan-t-registration-status',
        status: 'success'
      });
    } catch (error) {
      console.error('Registration submit failed', error);
      formFrame.postMessage({
        type: 'plan-t-registration-status',
        status: 'error',
        message: 'ההרשמה לא נשלחה. נסו שוב או פנו לתמיכה.'
      });
    }
  });
});
