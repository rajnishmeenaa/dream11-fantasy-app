/**
 * Brand Injector
 * Injects brand settings from BRAND_CONFIG into the DOM dynamically.
 */
document.addEventListener("DOMContentLoaded", () => {
  const cfg = window.BRAND_CONFIG || {};

  // Update Page Title
  document.title = `${cfg.brandName} | ${cfg.tagline}`;

  // Update Brand Names in DOM
  document.querySelectorAll(".brand-name-text").forEach(el => {
    el.textContent = cfg.brandName;
  });

  // Update Taglines
  document.querySelectorAll(".brand-tagline-text").forEach(el => {
    el.textContent = cfg.tagline;
  });

  // Update Slogan
  document.querySelectorAll(".brand-slogan-text").forEach(el => {
    el.textContent = cfg.slogan;
  });

  // Update Currencies
  document.querySelectorAll(".currency-symbol").forEach(el => {
    el.textContent = cfg.currencySymbol;
  });

  // Support Email
  document.querySelectorAll(".brand-support-email").forEach(el => {
    el.textContent = cfg.supportEmail;
  });
});
