import { useState } from 'react'
import './App.css'
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { Card } from 'primereact/card';

interface ISearchResult {
    startIndex: number;
    endIndex: number;
    probability: number;
}

function App() {
    const [originalText, setOriginalText] = useState('ты возьми корзину прежде чем набрать продукты');
    const [textToSearch, setTextToSearch] = useState('звонить');

    const [loadSearch, setLoadSearch] = useState(false);
    const [searchResult, setSearchResult] = useState<ISearchResult>(null);
    const [searchText, setSearchText] = useState('');

    async function onSearch() {
        try {
            setLoadSearch(true);

            const response = await fetch('http://localhost:5151/search', {
                method: 'POST',
                body: JSON.stringify({
                    document: originalText,
                    word: textToSearch,
                }),
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const searchResult: ISearchResult = await response.json();
            // защита от дурака
            if (
                searchResult.startIndex < 0
                || searchResult.startIndex > originalText.length
                || searchResult.endIndex > originalText.length
            ) {
                alert('Что-то не так с индексами start-end');
                return;
            }
            setSearchText(originalText);
            setSearchResult(searchResult);
        } finally {
            setLoadSearch(false);
        }
    }

    function onReset() {
        setSearchResult(null);
    }

    return (
        <main>
            <Card title="Семантический текстовый поиск">
                <p className="m-0">
                    Система семантического текстового поиска слов (словосочетаний), учитывающую не только точное
                    написание, но и смысловое значение.
                    Результатом должно быть определение позиции найденного слова/словосочетания в тексте и оценка
                    вероятности совпадения.
                </p>
            </Card>

            <div className='grid-input'>
                <div className="textarea">
                    <InputTextarea
                        value={originalText}
                        onChange={(e) => setOriginalText(e.target.value)}
                        rows={5}
                        cols={30}
                        placeholder={'Текст в котором ищем'}
                    />
                </div>
                <div className="controls">
                    <InputText
                        value={textToSearch}
                        onChange={(e) => setTextToSearch(e.target.value)}
                        placeholder={'Слова для поиска'}
                    />
                    <Button
                        label={loadSearch ? 'Поиск...' : 'Найти'}
                        onClick={onSearch}
                        disabled={!textToSearch || !originalText}
                    />
                    {Boolean(searchResult) && (
                        <Button
                            label="Сбросить"
                            severity="secondary"
                            onClick={onReset}
                        />
                    )}
                </div>
            </div>

            {Boolean(searchResult) && (
                <div className='search-result'>
                    <Card
                        title={`Вероятность совпадения ${Number(searchResult.probability * 100).toFixed(2)}%`}
                        subTitle={`Позиция ${searchResult.startIndex}-${searchResult.endIndex}`}
                    >
                        <p className="m-0">
                            {searchText.slice(0, searchResult.startIndex)}
                            <span className='highlight'>{searchText.slice(searchResult.startIndex, searchResult.endIndex + 1)}</span>
                            {searchText.slice(searchResult.endIndex + 1)}
                        </p>
                    </Card>
                </div>
            )}
        </main>
    );
}

export default App;
