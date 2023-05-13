<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	let ssn = '';
	let pid = '';
	let patient = {};
	let provider = {};
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
			const res = await fetch('http://localhost:8888/patient/' + ssn);
			const { patient: patientData } = await res.json();
			patient = patientData;

			const res2 = await fetch('http://localhost:8888/patient/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData.slice(-5);
		}

		if (!ssn && pid) {
			const res = await fetch('http://localhost:8888/provider/' + pid);
			const { provider: providerData } = await res.json();
			provider = providerData;

			const res2 = await fetch('http://localhost:8888/provider/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData.slice(-5);
		}
	});

	// Use a reactive statement to automatically update the `isLoading` variable
	let isLoading = true;
	$: isLoading = Object.keys(provider).length === 0 && Object.keys(patient).length === 0;
</script>

{#if isLoading}
	<p>Loading...</p>
{:else if Object.keys(provider).length > 0}
	<h1>My Provider Profile</h1>
	<div class="cards-container">
		<div class="left-cards">
			<div class="card">
				<h2><i class="fas fa-user" /> Personal Information</h2>
				<p><strong>Name:</strong> {provider.name}</p>
				<p><strong>Gender:</strong> {provider.gender}</p>
				<p><strong>Speciality:</strong> {provider.speciality}</p>
			</div>
			<div class="card">
				<h2><i class="fas fa-hospital" /> Organization Information</h2>
				<p><strong>Name:</strong> {provider.organization.name}</p>
				<p><strong>Phone:</strong> {provider.organization.phone}</p>
				<p>
					<strong>Address:</strong>
					{provider.organization.address}, {provider.organization.city},
					{provider.organization.state}
					{provider.organization.zip}
				</p>
			</div>
		</div>
		<div class="right-card">
			<div class="card">
				<div class="card-header">
					<h2><i class="fas fa-notes-medical" /> Last Encounters</h2>
					<a href="/encounters"> See all</a>
				</div>
				{#if encounters.length === 0}
					<p>No encounters found.</p>
				{/if}
				{#each encounters as encounter}
					<p>
						{new Date(encounter.start).toLocaleDateString()}: {encounter.description}
					</p>
				{/each}
			</div>
		</div>
	</div>
{:else if Object.keys(patient).length > 0}
	<h1>My Patient Profile</h1>
	<div class="cards-container">
		<div class="left-cards">
			<div class="card">
				<h2><i class="fas fa-user" /> Personal Information</h2>
				<p><strong>Name:</strong> {patient.prefix} {patient.first} {patient.last}</p>
				<p><strong>Birthdate:</strong> {patient.birthdate}</p>
				<p><strong>SSN:</strong> {patient.ssn}</p>
				<p><strong>Gender:</strong> {patient.gender}</p>
			</div>
			<div class="card">
				<h2><i class="fas fa-map-marker-alt" /> Contact Information</h2>
				<p>
					<strong>Address:</strong>
					{patient.address}, {patient.city}, {patient.state}
					{patient.zip}
				</p>
			</div>
		</div>
		<div class="right-card">
			<div class="card">
				<div class="card-header">
					<h2><i class="fas fa-notes-medical" /> Last Encounters</h2>
					<a href="/encounters"> See all</a>
				</div>
				{#if encounters.length == 0}
					<p>No encounters found.</p>
				{/if}
				{#each encounters as encounter}
					<p>
						{new Date(encounter.start).toLocaleDateString()}: {encounter.description}
					</p>
				{/each}
			</div>
		</div>
	</div>
{/if}

<style>
	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.cards-container {
		display: flex;
	}

	.left-cards {
		flex: 1;
		margin-right: 1.5rem;
	}

	.right-card {
		flex: 2;
	}

	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
	}

	.card h2 {
		margin: 10px;
		font-size: 1.2rem;
	}

	.card p {
		margin: 10px;
	}

	.fas {
		margin-right: 10px;
	}

	.right-card .card p {
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	a {
		color: #000000;
		margin-right: 1rem;
	}
	a:hover {
		color: #000000;
		text-decoration: none;
		cursor: pointer;
	}
</style>
