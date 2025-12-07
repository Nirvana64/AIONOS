/**
 * AIONOS - Main Application
 * Handles timeline rendering, filtering, and interactions
 */

// ============================================
// State Management
// ============================================

const state = {
    events: [],
    filteredEvents: [],
    stats: null,
    currentTheme: 'light',
    filters: {
        category: '',
        yearFrom: null,
        yearTo: null,
        search: ''
    }
};

// ============================================
// DOM Elements
// ============================================

const elements = {
    timeline: document.getElementById('timeline'),
    loading: document.getElementById('loading'),
    noResults: document.getElementById('no-results'),

    // Filters
    categoryFilter: document.getElementById('category-filter'),
    yearFrom: document.getElementById('year-from'),
    yearTo: document.getElementById('year-to'),
    searchInput: document.getElementById('search-input'),
    resetFilters: document.getElementById('reset-filters'),

    // Stats
    totalEvents: document.getElementById('total-events'),
    yearRange: document.getElementById('year-range'),
    categoriesCount: document.getElementById('categories-count'),

    // Modal
    modalOverlay: document.getElementById('modal-overlay'),
    modal: document.getElementById('event-modal'),
    modalClose: document.getElementById('modal-close'),
    modalCategory: document.getElementById('modal-category'),
    modalTitle: document.getElementById('modal-title'),
    modalDate: document.getElementById('modal-date'),
    modalDescription: document.getElementById('modal-description'),
    modalSource: document.getElementById('modal-source'),

    // Theme
    themeToggle: document.getElementById('theme-toggle'),
    themeIcon: document.querySelector('.theme-icon')
};

// ============================================
// API Functions
// ============================================

const API_BASE = '/api';

async function fetchEvents(filters = {}) {
    const params = new URLSearchParams();

    if (filters.category) params.append('category', filters.category);
    if (filters.yearFrom) params.append('year_from', filters.yearFrom);
    if (filters.yearTo) params.append('year_to', filters.yearTo);
    if (filters.search) params.append('search', filters.search);

    const url = `${API_BASE}/events${params.toString() ? '?' + params.toString() : ''}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch events');
        const data = await response.json();
        return data.events || [];
    } catch (error) {
        console.error('Error fetching events:', error);
        return [];
    }
}

async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        if (!response.ok) throw new Error('Failed to fetch stats');
        return await response.json();
    } catch (error) {
        console.error('Error fetching stats:', error);
        return null;
    }
}

// ============================================
// Rendering Functions
// ============================================

function formatDate(event) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    let date = event.year.toString();

    if (event.month) {
        date = `${months[event.month - 1]} ${date}`;
    }

    if (event.day) {
        date = `${event.day} ${date}`;
    }

    return date;
}

function formatCategory(category) {
    // Capitalize first letter
    return category.charAt(0).toUpperCase() + category.slice(1);
}

function renderImportance(importance) {
    let dots = '';
    for (let i = 1; i <= 5; i++) {
        dots += `<span class="importance-dot ${i <= importance ? 'filled' : ''}"></span>`;
    }
    return dots;
}

function renderEventCard(event) {
    const card = document.createElement('div');
    card.className = 'event-card';
    card.dataset.eventId = event.id;

    card.innerHTML = `
        <div class="event-importance">
            ${renderImportance(event.importance || 3)}
        </div>
        <div class="event-header">
            <span class="event-category ${event.category}">${formatCategory(event.category)}</span>
        </div>
        <h3 class="event-title">${escapeHtml(event.title)}</h3>
        <p class="event-date">${formatDate(event)}</p>
        <p class="event-description">${escapeHtml(event.description || '')}</p>
    `;

    card.addEventListener('click', () => openModal(event));

    return card;
}

function renderTimeline(events) {
    elements.timeline.innerHTML = '';

    if (!events || events.length === 0) {
        elements.noResults.style.display = 'block';
        return;
    }

    elements.noResults.style.display = 'none';

    // Group events by year
    const eventsByYear = {};
    events.forEach(event => {
        const year = event.year;
        if (!eventsByYear[year]) {
            eventsByYear[year] = [];
        }
        eventsByYear[year].push(event);
    });

    // Sort years
    const years = Object.keys(eventsByYear).sort((a, b) => Number(a) - Number(b));

    // Render each year
    years.forEach(year => {
        // Year marker
        const yearMarker = document.createElement('div');
        yearMarker.className = 'timeline-year';
        yearMarker.innerHTML = `<span class="year-label">${year}</span>`;
        elements.timeline.appendChild(yearMarker);

        // Events for this year (sorted by month, day)
        const yearEvents = eventsByYear[year].sort((a, b) => {
            const monthA = a.month || 0;
            const monthB = b.month || 0;
            if (monthA !== monthB) return monthA - monthB;
            return (a.day || 0) - (b.day || 0);
        });

        yearEvents.forEach(event => {
            elements.timeline.appendChild(renderEventCard(event));
        });
    });
}

function renderStats(stats) {
    if (!stats) return;

    elements.totalEvents.textContent = stats.total_events || 0;

    if (stats.year_range && stats.year_range.min && stats.year_range.max) {
        elements.yearRange.textContent = `${stats.year_range.min}-${stats.year_range.max}`;
    }

    if (stats.events_by_category) {
        elements.categoriesCount.textContent = Object.keys(stats.events_by_category).length;
    }
}

// ============================================
// Modal Functions
// ============================================

function openModal(event) {
    elements.modalCategory.textContent = formatCategory(event.category);
    elements.modalCategory.className = `modal-category event-category ${event.category}`;
    elements.modalTitle.textContent = event.title;
    elements.modalDate.textContent = formatDate(event);
    elements.modalDescription.textContent = event.description || 'No description available.';

    if (event.source_url) {
        elements.modalSource.href = event.source_url;
        elements.modalSource.style.display = 'inline-flex';
    } else {
        elements.modalSource.style.display = 'none';
    }

    elements.modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    elements.modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

// ============================================
// Theme Functions
// ============================================

function setTheme(theme) {
    state.currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    // Icons are now handled via CSS display switching
    localStorage.setItem('aionos-theme', theme);
}

function toggleTheme() {
    setTheme(state.currentTheme === 'light' ? 'dark' : 'light');
}

function loadSavedTheme() {
    const savedTheme = localStorage.getItem('aionos-theme');
    if (savedTheme) {
        setTheme(savedTheme);
    }
}

// ============================================
// Filter Functions
// ============================================

function applyFilters() {
    state.filters = {
        category: elements.categoryFilter.value,
        yearFrom: elements.yearFrom.value ? parseInt(elements.yearFrom.value) : null,
        yearTo: elements.yearTo.value ? parseInt(elements.yearTo.value) : null,
        search: elements.searchInput.value.trim()
    };

    loadEvents();
}

function resetFilters() {
    elements.categoryFilter.value = '';
    elements.yearFrom.value = '';
    elements.yearTo.value = '';
    elements.searchInput.value = '';

    state.filters = {
        category: '',
        yearFrom: null,
        yearTo: null,
        search: ''
    };

    loadEvents();
}

// Debounce for search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============================================
// Utility Functions
// ============================================

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading() {
    elements.loading.style.display = 'flex';
    elements.timeline.style.display = 'none';
    elements.noResults.style.display = 'none';
}

function hideLoading() {
    elements.loading.style.display = 'none';
    elements.timeline.style.display = 'block';
}

// ============================================
// Main Functions
// ============================================

async function loadEvents() {
    showLoading();

    const events = await fetchEvents(state.filters);
    state.events = events;

    hideLoading();
    renderTimeline(events);
}

async function loadStats() {
    const stats = await fetchStats();
    state.stats = stats;
    renderStats(stats);
}

async function init() {
    // Load saved theme
    loadSavedTheme();

    // Set up event listeners
    elements.themeToggle.addEventListener('click', toggleTheme);

    elements.categoryFilter.addEventListener('change', applyFilters);
    elements.yearFrom.addEventListener('change', applyFilters);
    elements.yearTo.addEventListener('change', applyFilters);
    elements.searchInput.addEventListener('input', debounce(applyFilters, 300));
    elements.resetFilters.addEventListener('click', resetFilters);

    elements.modalClose.addEventListener('click', closeModal);
    elements.modalOverlay.addEventListener('click', (e) => {
        if (e.target === elements.modalOverlay) closeModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

    // Load data
    await Promise.all([loadEvents(), loadStats()]);

    console.log('🧠 AIONOS initialized');
}

// Start the app
document.addEventListener('DOMContentLoaded', init);
