<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	let ssn = '';
	let pid = '';
	/**
	 * @type {string | any[]}
	 */
	let encounters = [];

	onMount(async () => {
		ssn = localStorage.getItem('ssn');
		pid = localStorage.getItem('pid');

		if (!ssn && !pid) {
			goto('/');
		}

		if (ssn && !pid) {
			const res2 = await fetch('http://localhost:8888/patient/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData;
		}

		if (!ssn && pid) {
			const res2 = await fetch('http://localhost:8888/provider/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData;
		}
	});

	// Use a reactive statement to automatically update the `isLoading` variable
	let isLoading = true;
	$: isLoading = Object.keys(encounters).length === 0;

	let filter = '';
	let startDateFilter = '';
	let endDateFilter = '';
	let classFilter = '';

	async function handleFilterChange(event) {
		filter = event.target.value;
	}

	async function handleStartDateFilterChange(event) {
		startDateFilter = event.target.value;
	}

	async function handleEndDateFilterChange(event) {
		endDateFilter = event.target.value;
	}

	async function handleClassFilterChange(event) {
		classFilter = event.target.value;
	}

	async function updateEncounters() {
		let url = 'http://localhost:8888/';
		if (ssn && !pid) {
			url += 'patient/' + ssn + '/encounters';
		} else if (!ssn && pid) {
			url += 'provider/' + pid + '/encounters';
		}

		if (startDateFilter || endDateFilter) {
			url += `?start=${startDateFilter}&end=${endDateFilter}`;
		} else if (classFilter) {
			url += `?class=${classFilter}`;
		}

		const res2 = await fetch(url);
		const { encounters: encountersData } = await res2.json();
		encounters = encountersData;
	}

	function clearFilters() {
		filter = '';
		startDateFilter = '';
		endDateFilter = '';
		classFilter = '';
		updateEncounters();
	}
</script>

{#if isLoading}
	<p>Loading...</p>
{:else if Object.keys(encounters).length > 0}
	<div class="container">
		<div class="left-column">
			<h2>Filters</h2>
			<input
				type="text"
				placeholder="Search..."
				oninput={handleFilterChange}
				class="filter-input"
			/>
			<input
				type="date"
				placeholder="Start Date"
				oninput={handleStartDateFilterChange}
				class="filter-input"
			/>
			<input
				type="date"
				placeholder="End Date"
				oninput={handleEndDateFilterChange}
				class="filter-input"
			/>
			<select onchange={handleClassFilterChange} class="filter-input">
				<option value="">All Classes</option>
				<option value="wellness">Wellness</option>
				<option value="emergency">Emergency</option>
				<option value="outpatient">Outpatient</option>
				<option value="inpatient">Inpatient</option>
				<option value="ambulatory">Ambulatory</option>
				<option value="urgentcare">Urgent Care</option>
			</select>
			<button on:click={updateEncounters} class="search-button">Search</button>
			<button on:click={clearFilters} class="clear-button">Clear Filters</button>
		</div>
		<div class="right-column">
			<h1>Encounters</h1>
			{#each encounters as encounter}
				<div class="card">
					<h2>{encounter.description}</h2>
					<p><strong>Start:</strong> {new Date(encounter.start).toLocaleString()}</p>
					<p><strong>Stop:</strong> {new Date(encounter.stop).toLocaleString()}</p>
					<p><strong>Provider:</strong> {encounter.provider.name}</p>
					<p><strong>Speciality:</strong> {encounter.provider.speciality}</p>
					<p><strong>Organization:</strong> {encounter.organization.name}</p>
					<p><strong>Address:</strong> {encounter.organization.address}</p>
					<p><strong>Class:</strong> {encounter.encounter_class}</p>
				</div>
			{/each}
		</div>
	</div>
{:else}
	<p>No encounters found.</p>
{/if}

<style>
	.container {
		display: flex;
	}

	.left-column {
		flex-basis: 200px;
		margin-right: 1rem;
	}

	.right-column {
		flex-grow: 1;
	}

	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	.filter-input,
	.search-button,
	.clear-button {
		display: block;
		width: 100%;
		box-sizing: border-box;
		margin-bottom: 10px;
		padding: 5px;
	}

	.search-button,
	.clear-button {
		cursor: pointer;
	}
</style>
